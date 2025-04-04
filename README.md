# yolo_v5-
# YOLOv5 Object Detection with Area Monitoring

A Python application that detects objects in real-time using YOLOv5, triggers alerts when objects enter a specified area, captures images, and sends email notifications.

## Features

- Real-time object detection using YOLOv5
- Configurable monitoring area (ROI)
- Visual and email alerts
- Image capture of detected objects
- Configurable confidence threshold
- Email notifications with attached images

## Installation

### Prerequisites
- Python 3.8-3.11
- Windows/Linux/macOS
- Webcam or video source

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/yolo_v5.git
   cd yolo_v5

## Troubleshooting

### Common Issues and Solutions

| Error Message | Solution |
|--------------|----------|
| `No module named...` | Install missing package: `pip install missing_module_name` |
| `CUDA out of memory` | 1. Use smaller model (`yolov5n`)<br>2. Reduce batch size<br>3. Close other GPU applications |
| Email sending fails | 1. Enable "Less secure apps" in Gmail<br>2. Use App Password instead of regular password<br>3. Check SMTP server settings |
| `Low FPS` (Poor performance) | 1. Reduce camera resolution<br>2. Use CPU instead of GPU (`device='cpu'`)<br>3. Lower detection confidence threshold |
| `AttributeError: module 'numpy' has no attribute...` | Downgrade NumPy: `pip install numpy==1.23.5` |
| `Webcam not detected` | 1. Check camera connection<br>2. Try different camera index (0, 1, etc.)<br>3. Verify OpenCV can access camera |
| `YOLOv5 model loading failed` | 1. Clear cache: `rm -rf ~/.cache/torch`<br>2. Reinstall: `pip install --force-reinstall ultralytics` |

### Additional Tips

1. **For GPU Users**:
   ```bash
   nvidia-smi  # Verify GPU is detected
   pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu118   
