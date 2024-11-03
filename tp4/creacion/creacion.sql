CREATE TABLE Accesos (
    AccesoId INT PRIMARY KEY IDENTITY(1,1),
    UsuarioId INT NOT NULL,
    FechaAcceso DATETIME NOT NULL,
    DireccionIP VARCHAR(45) NOT NULL
);

CREATE TABLE AuditoriaAccesos (
    AuditoriaId INT PRIMARY KEY IDENTITY(1,1),
    UsuarioId INT NOT NULL,
    FechaAcceso DATETIME NOT NULL,
    DireccionIP VARCHAR(45) NOT NULL,
    EstadoAcceso VARCHAR(20) NOT NULL -- Ejemplos: 'Exitoso', 'Fallido'
);