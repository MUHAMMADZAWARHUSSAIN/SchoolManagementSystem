
from django.db import models
from app.common.models import TimeStampedModel

import uuid

#! Represents a unique class within the school system
class Class(TimeStampedModel):
    # Point 1: Using a unique and indexed name field with maximum length constraint.
    name = models.CharField(max_length=50, unique=True, db_index=True,null=True)
    
    # Point 1, 6: Adding a `PositiveIntegerField` for label, which avoids nullable fields for performance.
    # If label is frequently queried, db_index is added.
    label = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    
    # Point 5: Nullable text field, only when description is optional. Avoid NULL when possible.
    description = models.TextField(blank=True, null=True)

    # Point 10: Adding UUID for efficient primary key handling on large datasets.
    uuid = models.UUIDField(default=None,null=True, editable=False, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        # Point 3: Indexes improve performance on queries filtering by name or label.
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['label']),
        ]

    
   
#! Represents a department with a unique name.
class Department(TimeStampedModel):
    
     # Point 1: Unique and indexed field for department name.
    name = models.CharField(max_length=100, unique=True, db_index=True,null=True)
    
    # Point 10: UUID field for scalability, improving performance with distributed systems.
    uuid = models.UUIDField(default=None,null=True, editable=False, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]


#!Represents sections associated with a class.
class Section(TimeStampedModel):
    
    # Point 1: Name field can be left blank or null; indexed if frequently searched.
    name = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    
    # Point 2: ForeignKey relationship, cascading delete (ensure sections are deleted with class).
    section_of_class = models.ForeignKey(Class, on_delete=models.CASCADE, db_index=True)
    
    # Point 10: UUID for more scalable, unique identification.
    uuid = models.UUIDField(default=None,null=True, editable=False, unique=True, db_index=True)

    def __str__(self):
        return f"{self.section_of_class} - {self.name}"

    class Meta:
        # Point 3: Composite index on section and class.
        indexes = [
            models.Index(fields=['section_of_class', 'name']),
        ]


#!Represents subjects taught in a specific class.
class Subjects(TimeStampedModel):
   
    # Point 2: ForeignKey to class; db_index improves query performance.
    subject_class = models.ForeignKey(Class, on_delete=models.CASCADE, db_index=True)
    
    # Point 1: Using indexed CharField for frequent querying on subject type.
    subject_type = models.CharField(max_length=64, db_index=True)
    
    # Point 1: Added unique constraint to prevent duplicate subject names in the same class.
    name = models.CharField(max_length=264, unique=True)
    
    # Point 10: UUID for scalability across distributed systems.
    uuid = models.UUIDField(default=None,null=True, editable=False, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        # Point 3: Composite index for efficient filtering by class and subject type.
        indexes = [
            models.Index(fields=['subject_class', 'subject_type']),
        ]




class Course(TimeStampedModel):
    name = models.CharField(max_length=100)
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    schedule = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.class_enrolled}"

class Enrollment(TimeStampedModel):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)  # Assuming you have a Student model
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course}"

























#! Tracks information related to school leaving certificates.
class SchoolLeavingCertificate(TimeStampedModel):
   
     # Point 2: ForeignKey relationships with appropriate `related_name`.
    admission_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='slc_admission_class', db_index=True)
    last_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='slc_last_class', db_index=True)
    
    # Point 2, 8: Relationship with student model, db_index added for optimized filtering.
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, db_index=True)
    
    # Point 1: Date fields indexed to allow quick lookups by dates.
    admission_date = models.DateField(db_index=True)
    leaving_date = models.DateField(null=True, blank=True)
    
    # Point 1: Boolean fields and PositiveIntegerFields for performance.
    arrears_remaining = models.PositiveIntegerField(default=0)
    is_refunded = models.BooleanField(db_index=True)
    security_refunded = models.PositiveIntegerField(default=0)
    
    # Point 1: Indexed CharFields for high-performance querying.
    paid_to = models.CharField(max_length=255, db_index=True)
    received_by = models.CharField(max_length=255, db_index=True)
    refund_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    
    # Point 10: UUID field for scalability.
    uuid = models.UUIDField(default=None,null=True, editable=False, unique=True, db_index=True)

    def __str__(self):
        return f"{self.student} - {self.admission_class}"

    class Meta:
        # Point 3: Composite indexes to optimize common queries.
        indexes = [
            models.Index(fields=['student', 'admission_class']),
            models.Index(fields=['admission_date', 'is_refunded']),
            models.Index(fields=['paid_to', 'received_by']),
        ]
