from django.db import models

class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    filiere = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.prenom}"