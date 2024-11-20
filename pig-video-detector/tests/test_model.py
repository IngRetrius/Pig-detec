import unittest
import os
import torch
from ultralytics import YOLO
import cv2
import numpy as np
import time
from datetime import datetime
import pandas as pd

class TestYOLOModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test model and resources"""
        cls.results_dir = os.path.join(os.path.dirname(__file__), 'results')
        os.makedirs(cls.results_dir, exist_ok=True)
        
        # Configurar modelos
        cls.models = {
            'YOLOv8s': {
                'path': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yolov8s.pt'),
                'stats': {}
            },
            'YOLOv8xl': {
                'path': r'C:\Users\USUARIO1\Documents\desesperacion-web\yolov8x.pt',
                'stats': {}
            }
        }
        
        # Verificar modelos
        for model_name, model_info in cls.models.items():
            if os.path.exists(model_info['path']):
                print(f"\nModelo {model_name} encontrado en: {model_info['path']}")
                model_info['size_mb'] = os.path.getsize(model_info['path']) / (1024 * 1024)
            else:
                print(f"\nAdvertencia: Modelo {model_name} no encontrado en: {model_info['path']}")
        
        cls.conf_threshold = 0.25
        cls.selected_classes = [18, 19]  # sheep (18), cow (19)
        cls.class_names = {18: 'sheep', 19: 'cow'}
        
        # Buscar videos
        cls.uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'uploads')
        cls.test_videos = []
        
        if os.path.exists(cls.uploads_dir):
            cls.test_videos = [f for f in os.listdir(cls.uploads_dir) if f.endswith('.mp4')]
            print(f"\nVideos encontrados: {len(cls.test_videos)}")
            for video in cls.test_videos:
                print(f"- {video}")

    def generate_metrics_excel(self, all_stats, timestamp):
        """Generate comprehensive Excel with metrics for all videos and models"""
        excel_path = os.path.join(self.results_dir, f'comprehensive_metrics_{timestamp}.xlsx')
        
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            # Hoja 1: Métricas por Video y Modelo
            detailed_metrics = []
            
            for video_name, model_stats in all_stats.items():
                for model_name, stats in model_stats.items():
                    metrics = {
                        'Video': video_name,
                        'Modelo': model_name,
                        'Total Frames': stats['total_frames'],
                        'FPS Original': stats['fps'],
                        'Resolución': stats['resolution'],
                        'Duración (s)': stats['duration'],
                        'Total Detecciones': stats['total_detections'],
                        'Cerdos por Frame': stats['total_detections'] / stats['total_frames'],
                        'Tiempo Promedio (s)': np.mean(stats['processing_times']),
                        'FPS Efectivos': 1 / np.mean(stats['processing_times']),
                        'Confianza Promedio': np.mean(stats['confidences']) if stats['confidences'] else 0,
                        'Confianza Mínima': np.min(stats['confidences']) if stats['confidences'] else 0,
                        'Confianza Máxima': np.max(stats['confidences']) if stats['confidences'] else 0,
                        'Detecciones como Oveja': stats['classes']['sheep'],
                        'Detecciones como Vaca': stats['classes']['cow'],
                        'Memoria Usada (MB)': stats['memory_used'],
                        'Tamaño Modelo (MB)': self.models[model_name]['size_mb']
                    }
                    detailed_metrics.append(metrics)
            
            pd.DataFrame(detailed_metrics).to_excel(writer, sheet_name='Métricas Detalladas', index=False)
            
            # Hoja 2: Comparativa de Modelos (promediado por modelo)
            model_comparison = {}
            for model_name in self.models.keys():
                model_metrics = [m for m in detailed_metrics if m['Modelo'] == model_name]
                model_comparison[model_name] = {
                    'Promedio FPS': np.mean([m['FPS Efectivos'] for m in model_metrics]),
                    'Promedio Cerdos/Frame': np.mean([m['Cerdos por Frame'] for m in model_metrics]),
                    'Promedio Confianza': np.mean([m['Confianza Promedio'] for m in model_metrics]),
                    'Total Detecciones': sum([m['Total Detecciones'] for m in model_metrics]),
                    'Promedio Memoria (MB)': np.mean([m['Memoria Usada (MB)'] for m in model_metrics]),
                    'Tamaño Modelo (MB)': model_metrics[0]['Tamaño Modelo (MB)']
                }
            
            pd.DataFrame(model_comparison).transpose().to_excel(writer, sheet_name='Comparativa Modelos')
            
            # Formato
            workbook = writer.book
            for sheet in writer.sheets.values():
                sheet.set_column('A:Z', 15)

        return excel_path

    def process_video(self, video_path, model, model_name, timestamp):
        """Process a single video with given model"""
        video_name = os.path.basename(video_path)
        print(f"\nProcesando {video_name} con {model_name}")
        
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        output_path = os.path.join(
            self.results_dir, 
            f'processed_{os.path.splitext(video_name)[0]}_{model_name}_{timestamp}.mp4'
        )
        
        out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*'mp4v'),
            fps,
            (width, height)
        )
        
        stats = {
            'total_frames': total_frames,
            'fps': fps,
            'resolution': f"{width}x{height}",
            'duration': total_frames / fps,
            'total_detections': 0,
            'classes': {'sheep': 0, 'cow': 0},
            'processing_times': [],
            'confidences': [],
            'detections_per_frame': [],
            'memory_used': 0
        }
        
        try:
            frame_count = 0
            initial_memory = torch.cuda.memory_allocated() if torch.cuda.is_available() else 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                start_time = time.time()
                results = model(frame, conf=self.conf_threshold)
                process_time = time.time() - start_time
                stats['processing_times'].append(process_time)
                
                frame_detections = 0
                
                for r in results:
                    boxes = r.boxes
                    for box, cls, conf in zip(boxes.xyxy, boxes.cls, boxes.conf):
                        if int(cls) in self.selected_classes:
                            frame_detections += 1
                            stats['total_detections'] += 1
                            class_name = self.class_names[int(cls)]
                            stats['classes'][class_name] += 1
                            stats['confidences'].append(float(conf))
                            
                            x1, y1, x2, y2 = map(int, box.tolist())
                            color = (0, 255, 0) if int(cls) == 18 else (255, 0, 0)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                            label = f"Cerdo ({conf:.2f})"
                            cv2.putText(frame, label, (x1, y1-10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                stats['detections_per_frame'].append(frame_detections)
                
                info_text = [
                    f"{model_name} - Frame: {frame_count}/{total_frames}",
                    f"Cerdos en frame: {frame_detections}",
                    f"Tiempo: {process_time:.3f}s",
                    f"FPS: {1/process_time:.1f}"
                ]
                
                for i, text in enumerate(info_text):
                    y_pos = 30 + (i * 30)
                    cv2.putText(frame, text, (10, y_pos), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                out.write(frame)
                frame_count += 1
                
                if frame_count % 100 == 0:
                    print(f"Procesados {frame_count}/{total_frames} frames...")
            
            final_memory = torch.cuda.memory_allocated() if torch.cuda.is_available() else 0
            stats['memory_used'] = (final_memory - initial_memory) / (1024 * 1024)
            
            print(f"\nEstadísticas para {video_name} con {model_name}:")
            print(f"- Frames procesados: {frame_count}")
            print(f"- Total detecciones: {stats['total_detections']}")
            print(f"- Cerdos por frame: {stats['total_detections']/frame_count:.2f}")
            print(f"- FPS promedio: {1/np.mean(stats['processing_times']):.2f}")
            
        finally:
            cap.release()
            out.release()
        
        return stats, output_path

    def test_model_comparison(self):
        """Test and compare different YOLO models with multiple videos"""
        self.assertTrue(len(self.test_videos) > 0, "No se encontraron videos para procesar")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        all_stats = {}
        
        for video_name in self.test_videos:
            video_path = os.path.join(self.uploads_dir, video_name)
            all_stats[video_name] = {}
            
            for model_name, model_info in self.models.items():
                model = YOLO(model_info['path'])
                stats, output_path = self.process_video(video_path, model, model_name, timestamp)
                all_stats[video_name][model_name] = stats
        
        # Generar métricas comparativas
        metrics_path = self.generate_metrics_excel(all_stats, timestamp)
        print(f"\nMétricas comparativas guardadas en: {metrics_path}")

if __name__ == '__main__':
    unittest.main()