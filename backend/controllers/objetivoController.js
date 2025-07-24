// controllers/objetivoController.js
const { sql, poolPromise } = require('../config/db');

// Obtener todos los objetivos de un paciente
exports.obtenerObjetivos = async (req, res) => {
  const { idPaciente } = req.params;
  try {
    const pool = await poolPromise;
    const result = await pool.request()
      .input('idPaciente', sql.Int, idPaciente)
      .query('SELECT * FROM Objetivos WHERE idPaciente = @idPaciente');
    res.json(result.recordset);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Crear un objetivo
exports.crearObjetivo = async (req, res) => {
  const { idPaciente, texto } = req.body;
  try {
    const pool = await poolPromise;
    await pool.request()
      .input('idPaciente', sql.Int, idPaciente)
      .input('texto', sql.NVarChar, texto)
      .query('INSERT INTO Objetivos (idPaciente, texto, completado) VALUES (@idPaciente, @texto, 0)');
    res.json({ mensaje: 'Objetivo creado' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Actualizar objetivo (completar o editar texto)
exports.actualizarObjetivo = async (req, res) => {
  const { idObjetivo } = req.params;
  const { texto, completado } = req.body;
  try {
    const pool = await poolPromise;
    await pool.request()
      .input('idObjetivo', sql.Int, idObjetivo)
      .input('texto', sql.NVarChar, texto)
      .input('completado', sql.Bit, completado)
      .query('UPDATE Objetivos SET texto = @texto, completado = @completado WHERE idObjetivo = @idObjetivo');
    res.json({ mensaje: 'Objetivo actualizado' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// Eliminar objetivo
exports.eliminarObjetivo = async (req, res) => {
  const { idObjetivo } = req.params;
  try {
    const pool = await poolPromise;
    await pool.request()
      .input('idObjetivo', sql.Int, idObjetivo)
      .query('DELETE FROM Objetivos WHERE idObjetivo = @idObjetivo');
    res.json({ mensaje: 'Objetivo eliminado' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
