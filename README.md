# **Instructions pour l'environnement virtuel et l'exécution du code d'application**

Ce code utilise Python et plusieurs bibliothèques tierces. Pour exécuter le code d'application de manière isolée, il est recommandé de créer et d'activer un environnement virtuel. Les étapes suivantes vous guideront à travers le processus :

### **Créer un environnement virtuel**

1.   Assurez-vous d'avoir Python installé sur votre système. Vous pouvez vérifier en exécutant la commande suivante dans votre terminal :

2.   Ouvrez un terminal et naviguez jusqu'au répertoire où vous avez enregistré le code d'application.

```
python --version
```

3. Pour créer un nouvel environnement virtuel, exécutez la commande suivante :

```
python -m venv mon_environnement

```
Remplacez "mon_environnement" par le nom de votre choix pour l'environnement virtuel.

### **Activer l'environnement virtuel**
1. Sur Windows, exécutez la commande suivante pour activer l'environnement virtuel :

```
source env/Scripts/activate

```
Sur macOS/Linux, utilisez la commande suivante :


```
source mon_environnement/bin/activate

```
Remplacez "mon_environnement" par le nom de votre environnement virtuel.

2. Une fois l'environnement virtuel activé, vous verrez le nom de l'environnement virtuel s'afficher dans votre terminal, indiquant qu'il est actif.

### **Installer les dépendances**
1. Assurez-vous que vous êtes toujours dans le répertoire où vous avez enregistré le code d'application et que l'environnement virtuel est actif.

2. Pour installer les dépendances nécessaires, exécutez la commande suivante :


```
pip install -r requirements.txt
```

Cela installera toutes les bibliothèques tierces nécessaires à l'exécution du code d'application.

### **Exécuter le code d'application**
1. Assurez-vous d'être toujours dans le répertoire où vous avez enregistré le code d'application et que l'environnement virtuel est actif.

2. Exécutez le code d'application à l'aide de la commande suivante :


```
python nom_du_fichier.py

```
Remplacez "nom_du_fichier.py" par le nom réel du fichier Python contenant le code d'application.

3. Le code d'application sera exécuté, et vous verrez les messages d'état et les informations affichés dans votre terminal.

4. Les données extraites seront enregistrées dans des fichiers CSV dans le répertoire spécifié dans le code d'application.
