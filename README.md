# SSH Tools

Herramientas de terminal para gestionar conexiones SSH y transferencias SCP usando perfiles.

## Estructura

```text
├── bin/
│   ├── windows/
│   │   ├── ssh-client.bat
│   │   └── scp-client.bat
│   ├── linux/
│   │   ├── ssh-client.sh
│   │   └── scp-client.sh
│   └── mac/
│       ├── ssh-client.sh
│       └── scp-client.sh
├── src/
│   ├── ssh.py
│   ├── scp.py
│   └── profiles/
│       └── profiles.json   (ignorado en git)
└── README.md
```

## Perfiles

Los perfiles se definen manualmente en `src/profiles/profiles.json`:

```json
[
    {
        "name": "Mi Servidor",
        "host": "192.168.1.100",
        "user": "root",
        "port": 22,
        "private_key": "/ruta/a/mi/clave_privada"
    }
]
```

Cada perfil tiene: `name`, `host`, `user` y `port`. Opcionalmente se puede indicar `private_key` con la ruta absoluta a la **clave privada** SSH (por ejemplo `~/.ssh/id_rsa` o `~/.ssh/id_ed25519`); si se omite o se deja vacío, se usará la clave por defecto del sistema. **No indicar la clave pública** (`.pub`), sino la privada.

> Este archivo está en `.gitignore` ya que contiene datos de conexión personales.

## Uso

### Desde los scripts de sistema (recomendado)

**Windows:**

```bash
bin\windows\ssh-client.bat
bin\windows\scp-client.bat ./local.txt :/home/user/remote.txt
```

**Linux:**

```bash
./bin/linux/ssh-client.sh
./bin/linux/scp-client.sh ./local.txt :/home/user/remote.txt
```

**Mac:**

```bash
./bin/mac/ssh-client.sh
./bin/mac/scp-client.sh ./local.txt :/home/user/remote.txt
```

### Desde Python directamente

```bash
python src/ssh.py
python src/scp.py <pathOrigen> <pathDestino>
```

## SSH

Muestra los perfiles disponibles, eliges uno y se ejecuta:

```bash
ssh -p <puerto> <usuario>@<host>
```

## SCP

Transfiere archivos usando un perfil. Para indicar rutas remotas se usa el prefijo `:`. Si ninguna ruta lleva `:`, el destino se trata como remoto por defecto.

```bash
# Local a remoto
scp-client ./archivo.txt :/home/user/archivo.txt

# Remoto a local
scp-client :/var/log/app.log ./logs/

# Sin ":" -> destino es remoto
scp-client ./deploy.sh /opt/scripts/
```

Se ejecuta internamente:

```bash
scp -P <puerto> <origen> <usuario>@<host>:<destino>
```
