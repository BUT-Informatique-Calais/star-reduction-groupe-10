# SAÉ S3.C2 – Réduction d’étoiles en astrophotographie

## Auteurs

* Quentin Bossus
* Ayyoub Boudahba
* Lilian Deceuninck--Cappelaere

---

## Présentation du projet

Ce projet a pour objectif de développer une **application Python avec interface graphique (PyQt6)** permettant de traiter des images d’astrophotographie au format **FITS**, en particulier pour effectuer une **réduction des étoiles** afin de mieux mettre en valeur les galaxies.

L’application permet :

* d’importer une image FITS (monochrome ou couleur)
* d’afficher l’image originale
* d’appliquer un algorithme de réduction d’étoiles
* d’ajuster les paramètres via des sliders
* d’exporter l’image 

---

## Architecture du projet

Le projet suit une architecture **MVC (Modèle – Vue – Contrôleur)** :

* **Model (`ImageModel`)

  * Chargement des fichiers FITS
  * Prétraitement des données
  * Détection des étoiles
  * Algorithme de réduction d’étoiles

* **View (`ImageView`)

  * Interface graphique PyQt6
  * Affichage des images
  * Sliders et boutons

* **Controller (`ImageController`)

  * Gestion des événements utilisateur
  * Lien entre la vue et le modèle

* **Optimisation (`StarReductionThread`)

  * Thread séparé pour les calculs lourds afin d’éviter le gel de l’interface

---

## Méthodes utilisées

### 1. Chargement des images FITS

Les images sont chargées avec la bibliothèque **Astropy** (`astropy.io.fits`).

* Support des images FITS monochromes et couleur
* Conversion en `numpy.ndarray`
* Création d’une version en niveaux de gris pour la détection d’étoiles

### 2. Détection des étoiles

La détection des étoiles est réalisée avec :

* **DAOStarFinder** (bibliothèque `photutils`)
* Calcul des statistiques de fond avec `sigma_clipped_stats`

Les étoiles sont détectées une seule fois par image afin d’optimiser les performances.

### 3. Réduction des étoiles

1. Création d’un masque autour de chaque étoile détectée
2. Application d’un **filtre médian** sur l’image
3. Lissage du masque avec un flou gaussien
4. Interpolation entre l’image originale et l’image filtrée

###

---

## Optimisation des performances

Lors du développement de  l’application nous avons rencontraient des problèmes de lenteur et de gel de l’interface.

### Solution mise en place

* Déplacement du traitement lourd dans un **QThread (`StarReductionThread`)**
* Désactivation temporaire des sliders pendant le calcul
* Réutilisation des étoiles détectées entre deux traitements

Résultat :

* Interface fluide
* Temps de réponse fortement amélioré

---

## Difficultés rencontrées

### 1. Gestion des couleurs

* Altération des couleurs lors du traitement des images FITS couleur
* Confusion entre les formats **RGB** et **BGR** (OpenCV)



### 2. Images FITS non affichées

* Certaines images FITS apparaisaient noires

* Problèmes de normlisation des données

*  Solution :

* Normalisation correcte des données

* Traitement canal par canal pour les images couleur

### 3. Blocage de l’interface graphique

* Calculs trop lourds exécutés dans le thread principal

   Solution :

* Utilisation de `QThread` pour le traitement d’image

---

## Résultats obtenus

* Application fonctionnelle et stable
* Chargement et affichage corrects des images FITS
* Réduction d’étoiles visible et paramétrable
* Interface fluide grâce au threading

---


---

## Installation


### Virtual Environment

It is recommended to create a virtual environment before installing dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```


### Dependencies
```bash
pip install -r requirements.txt
```

Or install dependencies manually:
```bash
pip install [package-name]
```

## Usage


### Command Line
```bash
python main.py [arguments]
```

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependency list

## Examples files
Example files are located in the `examples/` directory. You can run the scripts with these files to see how they work.
- Example 1 : `examples/HorseHead.fits` (Black and whiteFITS image file for testing)
- Example 2 : `examples/test_M31_linear.fits` (Color FITS image file for testing)
- Example 3 : `examples/test_M31_raw.fits` (Color FITS image file for testing)
