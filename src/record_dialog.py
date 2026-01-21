import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QDialog, QTextEdit, QLabel,QSizePolicy
)
from PySide6.QtMultimedia import (
    QMediaCaptureSession,
    QAudioInput,
    QMediaRecorder,
    QMediaDevices,
    QAudioFormat,
    QMediaFormat
)
from PySide6.QtCore import QUrl,QDateTime
from pathlib import Path
import tempfile
from src.asr_pipeline import run_speech_to_task_pipeline
import ffmpeg
import librosa
import soundfile as sf
from PySide6.QtCore import QObject, QThread, Signal, Slot
import time
from src.control_unit import ControlUnit
from src.todo import Todo
import json

class Worker(QObject):
    finished = Signal()
    error = Signal(str)
    result = Signal(object)

    def __init__(self, output_file):
        super().__init__()
        self.output_file = output_file
    @Slot()
    def run(self):
        try:
            # 🔹 YOUR LONG-RUNNING CODE HERE
            ffmpeg.input(self.output_file).output(self.output_file.replace(".mp4",".wav"), ac=1).overwrite_output().run()
            x,samplerate = librosa.load(self.output_file.replace(".mp4",".wav"))
            sf.write(self.output_file.replace(".mp4",".wav"), x, samplerate)
            task=run_speech_to_task_pipeline(self.output_file.replace(".mp4",".wav"))
            # 🔹 END CODE
            self.result.emit(task)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()




class RecordDialog(QDialog):
    def __init__(self,database, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Audio Recorder")
        self.database=database

        # UI
        self.status_label = QLabel("Ready")
        self.start_button = QPushButton("Start Recording")
        self.stop_button = QPushButton("Stop Recording")
        self.result_field = QTextEdit()
        self.result_field.setPlaceholderText("Recording result will appear here")
        self.create_todo_button = QPushButton("Create Todo")
        self.result_field.setText("""{"name": "", "tag": "", "status": "", "start_date": "", "end_date": ""}""")


        self.result_field.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.stop_button.setEnabled(False)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        layout.addWidget(self.result_field, stretch=1)

        layout.addWidget(self.create_todo_button)

        # Audio setup
        self.capture_session = QMediaCaptureSession()

        self.audio_input = QAudioInput(QMediaDevices.defaultAudioInput())
        self.capture_session.setAudioInput(self.audio_input)

        self.recorder = QMediaRecorder()
        self.capture_session.setRecorder(self.recorder)

        temp_dir = Path(tempfile.gettempdir())
        file_path = temp_dir / "recording.mp4"
        self.output_file = str(file_path)

        self.recorder.setAudioChannelCount(1)


        # Mono format
        #audio_format = QAudioFormat()
        #audio_format.setSampleRate(44100)
        #audio_format.setChannelCount(1)
        #audio_format.setSampleFormat(QAudioFormat.Int16)
        #self.audio_input.setFormat(audio_format)

        # Connections
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.recorder.recorderStateChanged.connect(self.on_state_changed)
        self.create_todo_button.clicked.connect(self.on_create_todo_button_clicked)


    def start_recording(self):

        print(self.recorder.audioChannelCount())
        self.recorder.setOutputLocation(QUrl.fromLocalFile(self.output_file))
        self.recorder.record()

        self.status_label.setText("Recording...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_recording(self):
        self.recorder.stop()

    def on_state_changed(self, state):
        if state == QMediaRecorder.StoppedState:
            self.status_label.setText("Recording stopped")
            #self.result_field.setText(f"Saved to {self.output_file}")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

            ###START THREAD
            # Create thread and worker
            self.thread = QThread()
            self.worker = Worker(self.output_file)

            # Move worker to thread
            self.worker.moveToThread(self.thread)

            # Connect signals
            self.thread.started.connect(self.worker.run)
            self.worker.result.connect(self.on_worker_result)
            self.worker.error.connect(self.on_worker_error)

            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            # Start thread
            self.thread.start()
    def on_worker_result(self, result):
        self.result_field.setText(json.dumps(result))
        #self.status_label.setText("Done")

    def on_worker_error(self, message):
        #self.status_label.setText("Error")
        self.result_field.setText(message)
    def on_create_todo_button_clicked(self):
        cu=ControlUnit(self.database)

        task_json=json.loads(self.result_field.toPlainText())
        name=task_json["name"]
        start_date=task_json["start_date"]
        end_date=task_json["end_date"]
        tag=task_json["tag"]
        status=task_json["status"]
        date_created = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm")
        print(task_json)



        td=Todo( name,start_date, end_date,  date_created, 0, tag)
        td.updateStatus(status)
        cu.AddTodo(td)

        self.close()

