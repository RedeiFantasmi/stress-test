# Programme Python de test de la saturation réseau

## **Usage**

Ce programme sert à tester la charge réseau sur des ports TCP spécifiés. Il prend en entrée un paramétrage (port 1, port2, port3, durée de test, hôte) et renvoie en sortie les temps de réponses au ping qu'il a observés

## **Code externe utilisé**

### Librairies python

- time - ([time](https://docs.python.org/fr/3/library/time.html), [sleep](https://docs.python.org/fr/3/library/time.html#time.time))
- os - ([getcwd](https://docs.python.org/3/library/os.html#os.getcwd))
- pymysql - ([documentation](https://pypi.org/project/PyMySQL/#documentation))
- subprocess - ([documentation](https://docs.python.org/3/library/subprocess.html))
- threading - ([documentation](https://docs.python.org/3/library/subprocess.html))

### Librairies externes

- [nethogs](https://github.com/raboof/nethogs)
- [tcpping](https://github.com/yantisj/tcpping)