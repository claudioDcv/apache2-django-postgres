from django.apps import AppConfig


class MedicalconsultationConfig(AppConfig):
    name = 'medicalConsultation'
    verbose_name = "Consulta Médica"

    def ready(self):
        import medicalConsultation.signals  # noqa
