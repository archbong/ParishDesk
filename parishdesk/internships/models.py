from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Church


class InternshipProgram(models.Model):
    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="internship_programs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_weeks = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class InternshipApplication(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="applications"
    )

    applicant_name = models.CharField(max_length=255)
    applicant_email = models.EmailField()
    phone = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    reviewed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    applied_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.applicant_name} - {self.program.title}"
class InternshipAssignment(models.Model):
    application = models.OneToOneField(
        InternshipApplication, on_delete=models.CASCADE, related_name="assignment"
    )
    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="internship_assignments"
    )
    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Assignment for {self.application.applicant_name} to {self.assigned_to.username if self.assigned_to else 'Unassigned'}"

class InternshipReport(models.Model):
    assignment = models.ForeignKey(
        InternshipAssignment, on_delete=models.CASCADE, related_name="reports"
    )
    report_date = models.DateField(default=timezone.now)
    content = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report for {self.assignment.application.applicant_name} on {self.report_date}"

class InternshipFeedback(models.Model):
    report = models.ForeignKey(
        InternshipReport, on_delete=models.CASCADE, related_name="feedbacks"
    )
    provided_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    comments = models.TextField()
    rating = models.PositiveIntegerField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback by {self.provided_by.username if self.provided_by else 'Anonymous'} on {self.report}"
    
class InternshipCertificate(models.Model):
    assignment = models.OneToOneField(
        InternshipAssignment, on_delete=models.CASCADE, related_name="certificate"
    )
    certificate_file = models.FileField(upload_to="internship_certificates/")
    issued_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Certificate for {self.assignment.application.applicant_name}"
    
class InternshipEvaluation(models.Model):
    assignment = models.ForeignKey(
        InternshipAssignment, on_delete=models.CASCADE, related_name="evaluations"
    )
    evaluator = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    overall_rating = models.PositiveIntegerField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Evaluation by {self.evaluator.username if self.evaluator else 'Anonymous'} for {self.assignment.application.applicant_name}"

class InternshipOrientation(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="orientations"
    )
    orientation_date = models.DateField()
    location = models.CharField(max_length=255)
    agenda = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Orientation for {self.program.title} on {self.orientation_date}"
    
class InternshipExitInterview(models.Model):
    assignment = models.OneToOneField(
        InternshipAssignment, on_delete=models.CASCADE, related_name="exit_interview"
    )
    interview_date = models.DateField(default=timezone.now)
    feedback = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Exit Interview for {self.assignment.application.applicant_name}"

class InternshipMentor(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="mentors"
    )
    mentor = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="internship_mentorships"
    )
    assigned_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Mentor {self.mentor.username if self.mentor else 'Unassigned'} for {self.program.title}"
    
class InternshipSkillDevelopment(models.Model):
    assignment = models.ForeignKey(
        InternshipAssignment, on_delete=models.CASCADE, related_name="skill_developments"
    )
    skill_name = models.CharField(max_length=255)
    description = models.TextField()
    achieved_at = models.DateField(default=timezone.now)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Skill {self.skill_name} for {self.assignment.application.applicant_name}"
    
class InternshipAttendance(models.Model):
    assignment = models.ForeignKey(
        InternshipAssignment, on_delete=models.CASCADE, related_name="attendances"
    )
    attendance_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[("PRESENT", "Present"), ("ABSENT", "Absent")])

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Attendance on {self.attendance_date} for {self.assignment.application.applicant_name}"
    
class InternshipProject(models.Model):
    assignment = models.ForeignKey(
        InternshipAssignment, on_delete=models.CASCADE, related_name="projects"
    )
    project_title = models.CharField(max_length=255)
    description = models.TextField()
    completed_at = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Project {self.project_title} for {self.assignment.application.applicant_name}"
    
class InternshipResource(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="resources"
    )
    resource_name = models.CharField(max_length=255)
    resource_file = models.FileField(upload_to="internship_resources/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Resource {self.resource_name} for {self.program.title}"
    
class InternshipEvaluationCriterion(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="evaluation_criteria"
    )
    criterion_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Criterion {self.criterion_name} for {self.program.title}"
    
class InternshipAlumni(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="alumni"
    )
    alumni_name = models.CharField(max_length=255)
    alumni_email = models.EmailField()
    phone = models.CharField(max_length=20)
    graduation_year = models.PositiveIntegerField()

    def __str__(self):
        return f"Alumni {self.alumni_name} from {self.program.title}"
    
class InternshipSurvey(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="surveys"
    )
    survey_title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Survey {self.survey_title} for {self.program.title}"
    
class InternshipSurveyResponse(models.Model):
    survey = models.ForeignKey(
        InternshipSurvey, on_delete=models.CASCADE, related_name="responses"
    )
    respondent_name = models.CharField(max_length=255)
    respondent_email = models.EmailField()
    responses = models.TextField()

    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Response by {self.respondent_name} for {self.survey.survey_title}"
    
class InternshipFunding(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="fundings"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=255)
    received_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Funding of {self.amount} from {self.source} for {self.program.title}"
    
class InternshipBudget(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="budgets"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Budget for {self.program.title}: {self.allocated_amount}/{self.total_amount}"
    
class InternshipGoal(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="goals"
    )
    goal_description = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Goal for {self.program.title}: {self.goal_description[:50]}..."
    
class InternshipOutcome(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="outcomes"
    )
    outcome_description = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Outcome for {self.program.title}: {self.outcome_description[:50]}..."
    
class InternshipChallenge(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="challenges"
    )
    challenge_description = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Challenge for {self.program.title}: {self.challenge_description[:50]}..."
    
class InternshipSuccessStory(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="success_stories"
    )
    story_title = models.CharField(max_length=255)
    story_content = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Success Story for {self.program.title}: {self.story_title}"
    
class InternshipNetworkingEvent(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="networking_events"
    )
    event_title = models.CharField(max_length=255)
    event_date = models.DateField()
    location = models.CharField(max_length=255)
    agenda = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Networking Event for {self.program.title}: {self.event_title}"
    
class InternshipReflection(models.Model):
    assignment = models.ForeignKey(
        InternshipAssignment, on_delete=models.CASCADE, related_name="reflections"
    )
    reflection_date = models.DateField(default=timezone.now)
    content = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reflection for {self.assignment.application.applicant_name} on {self.reflection_date}"
    
class InternshipFollowUp(models.Model):
    application = models.ForeignKey(
        InternshipApplication, on_delete=models.CASCADE, related_name="follow_ups"
    )
    follow_up_date = models.DateField(default=timezone.now)
    notes = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Follow Up for {self.application.applicant_name} on {self.follow_up_date}"
    
class InternshipOrientationMaterial(models.Model):
    orientation = models.ForeignKey(
        InternshipOrientation, on_delete=models.CASCADE, related_name="materials"
    )
    material_name = models.CharField(max_length=255)
    material_file = models.FileField(upload_to="internship_orientation_materials/")

    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Material {self.material_name} for Orientation on {self.orientation.orientation_date}"
    
class InternshipClosingCeremony(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="closing_ceremonies"
    )
    ceremony_date = models.DateField()
    location = models.CharField(max_length=255)
    agenda = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Closing Ceremony for {self.program.title} on {self.ceremony_date}"

class InternshipAlumniEvent(models.Model):
    alumni = models.ForeignKey(
        InternshipAlumni, on_delete=models.CASCADE, related_name="events"
    )
    event_title = models.CharField(max_length=255)
    event_date = models.DateField()
    location = models.CharField(max_length=255)
    agenda = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Alumni Event for {self.alumni.alumni_name}: {self.event_title}"
    
class InternshipJobPlacement(models.Model):
    alumni = models.ForeignKey(
        InternshipAlumni, on_delete=models.CASCADE, related_name="job_placements"
    )
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Job Placement for {self.alumni.alumni_name}: {self.job_title} at {self.company_name}"
    
class InternshipScholarship(models.Model):
    alumni = models.ForeignKey(
        InternshipAlumni, on_delete=models.CASCADE, related_name="scholarships"
    )
    scholarship_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    awarded_at = models.DateField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Scholarship for {self.alumni.alumni_name}: {self.scholarship_name} of {self.amount}"
    
class InternshipPublication(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="publications"
    )
    publication_title = models.CharField(max_length=255)
    publication_file = models.FileField(upload_to="internship_publications/")
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Publication {self.publication_title} for {self.program.title}"
    
class InternshipMediaCoverage(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="media_coverages"
    )
    media_title = models.CharField(max_length=255)
    media_link = models.URLField()
    coverage_date = models.DateField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Media Coverage {self.media_title} for {self.program.title}"

class InternshipPartnership(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="partnerships"
    )
    partner_name = models.CharField(max_length=255)
    partner_contact = models.CharField(max_length=255)
    partnership_details = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Partnership with {self.partner_name} for {self.program.title}"
    
class InternshipEvent(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="events"
    )
    event_title = models.CharField(max_length=255)
    event_date = models.DateField()
    location = models.CharField(max_length=255)
    agenda = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Event {self.event_title} for {self.program.title}"
    
class InternshipNewsletter(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="newsletters"
    )
    newsletter_title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Newsletter {self.newsletter_title} for {self.program.title}"
    
class InternshipBlogPost(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="blog_posts"
    )
    post_title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Blog Post {self.post_title} for {self.program.title}"
    
class InternshipVideo(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="videos"
    )
    video_title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="internship_videos/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Video {self.video_title} for {self.program.title}"
    
class InternshipPodcast(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="podcasts"
    )
    podcast_title = models.CharField(max_length=255)
    podcast_file = models.FileField(upload_to="internship_podcasts/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Podcast {self.podcast_title} for {self.program.title}"
    
class InternshipWebinar(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="webinars"
    )
    webinar_title = models.CharField(max_length=255)
    webinar_link = models.URLField()
    scheduled_at = models.DateTimeField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Webinar {self.webinar_title} for {self.program.title}"
    
class InternshipWorkshop(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="workshops"
    )
    workshop_title = models.CharField(max_length=255)
    workshop_date = models.DateField()
    location = models.CharField(max_length=255)
    agenda = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Workshop {self.workshop_title} for {self.program.title}"
    
class InternshipCertificateTemplate(models.Model):
    program = models.ForeignKey(
        InternshipProgram, on_delete=models.CASCADE, related_name="certificate_templates"
    )
    template_name = models.CharField(max_length=255)
    template_file = models.FileField(upload_to="internship_certificate_templates/")

    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Certificate Template {self.template_name} for {self.program.title}"