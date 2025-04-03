from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from .utils import process_student_qr, visual_cryptography_decrypt
from django.http import HttpResponse, FileResponse
from PIL import Image
import io
import os
from django.conf import settings

def landing_page(request):
    return HttpResponse("""
    <html>
        <head>
            <title>Student QR System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                }
                .container {
                    background-color: #f5f5f5;
                    padding: 20px;
                    border-radius: 5px;
                }
                h1 {
                    color: #333;
                }
                .endpoints {
                    background-color: white;
                    padding: 15px;
                    border-radius: 5px;
                    margin-top: 20px;
                }
                code {
                    background-color: #eee;
                    padding: 2px 5px;
                    border-radius: 3px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Student QR System</h1>
                <p>This is a REST API for managing student QR codes.</p>
                
                <div class="endpoints">
                    <h2>Available Endpoints:</h2>
                    <ul>
                        <li><code>/api/students/</code> - List and create students</li>
                        <li><code>/api/students/{id}/</code> - Retrieve, update, or delete a specific student</li>
                        <li><code>/admin/</code> - Admin interface</li>
                    </ul>
                </div>
                
                <p>For API documentation, visit <a href="/api/">API Root</a></p>
            </div>
        </body>
    </html>
    """)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def perform_create(self, serializer):
        # Save student first
        student = serializer.save()
        # Generate QR code and encrypt
        process_student_qr(student)
    
    @action(detail=True, methods=['get'])
    def shares(self, request, pk=None):
        """Return both shares for a student"""
        student = self.get_object()
        
        # Get full paths to shares
        share1_path = os.path.join(settings.MEDIA_ROOT, student.share1.name)
        share2_path = os.path.join(settings.MEDIA_ROOT, student.share2.name)
        
        # Open and prepare both shares
        share1_img = Image.open(share1_path)
        share2_img = Image.open(share2_path)
        
        # Convert to bytes
        share1_io = io.BytesIO()
        share2_io = io.BytesIO()
        
        share1_img.save(share1_io, format='PNG')
        share2_img.save(share2_io, format='PNG')
        
        share1_io.seek(0)
        share2_io.seek(0)
        
        # Return both shares
        return Response({
            'share1': f'/media/{student.share1.name}',
            'share2': f'/media/{student.share2.name}'
        })
    
    @action(detail=True, methods=['get'])
    def decrypt(self, request, pk=None):
        """Decrypt and return the combined QR code"""
        student = self.get_object()
        
        # Get full paths to shares
        share1_path = os.path.join(settings.MEDIA_ROOT, student.share1.name)
        share2_path = os.path.join(settings.MEDIA_ROOT, student.share2.name)
        
        # Decrypt by combining shares
        decrypted_img = visual_cryptography_decrypt(share1_path, share2_path)
        
        # Prepare image for HTTP response
        img_io = io.BytesIO()
        decrypted_img.save(img_io, format='PNG')
        img_io.seek(0)
        
        return FileResponse(img_io, content_type='image/png')