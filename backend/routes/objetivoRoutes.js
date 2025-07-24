// routes/objetivoRoutes.js
const express = require('express');
const router = express.Router();
const objetivoController = require('../controllers/objetivoController');
const { verifyToken } = require('../middleware/authMiddleware');

router.get('/:idPaciente', verifyToken, objetivoController.obtenerObjetivos);
router.post('/', verifyToken, objetivoController.crearObjetivo);
router.patch('/:idObjetivo', verifyToken, objetivoController.actualizarObjetivo);
router.delete('/:idObjetivo', verifyToken, objetivoController.eliminarObjetivo);

module.exports = router;
