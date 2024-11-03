CREATE PROCEDURE AuditarAccesos
AS
BEGIN
    DECLARE @AccesoId INT
    DECLARE @UsuarioId INT
    DECLARE @FechaAcceso DATETIME
    DECLARE @DireccionIP VARCHAR(45)
    DECLARE @EstadoAcceso VARCHAR(20)

    DECLARE cursor_accesos CURSOR FOR
        SELECT TOP 100 AccesoId, UsuarioId, FechaAcceso, DireccionIP
        FROM Accesos
        ORDER BY FechaAcceso DESC

    BEGIN TRANSACTION

    BEGIN TRY
        OPEN cursor_accesos

        FETCH NEXT FROM cursor_accesos INTO @AccesoId, @UsuarioId, @FechaAcceso, @DireccionIP

        WHILE @@FETCH_STATUS = 0
        BEGIN
            DECLARE @IntentosFallidos INT
            SELECT @IntentosFallidos = COUNT(*)
            FROM AuditoriaAccesos
            WHERE DireccionIP = @DireccionIP
              AND EstadoAcceso = 'Fallido'
              AND FechaAcceso >= DATEADD(HOUR, -24, @FechaAcceso)

            IF @IntentosFallidos >= 3
                SET @EstadoAcceso = 'Fallido'
            ELSE
                SET @EstadoAcceso = 'Exitoso'

            INSERT INTO AuditoriaAccesos (UsuarioId, FechaAcceso, DireccionIP, EstadoAcceso)
            VALUES (@UsuarioId, @FechaAcceso, @DireccionIP, @EstadoAcceso)

            FETCH NEXT FROM cursor_accesos INTO @AccesoId, @UsuarioId, @FechaAcceso, @DireccionIP
        END

        CLOSE cursor_accesos
        DEALLOCATE cursor_accesos

        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION

        IF CURSOR_STATUS('global', 'cursor_accesos') >= 0
        BEGIN
            CLOSE cursor_accesos
            DEALLOCATE cursor_accesos
        END

        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE()
        RAISERROR(@ErrorMessage, 16, 1)
    END CATCH
END