import express from 'express';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

// Resolve __dirname for ES module compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Render the index page
app.get('/', (req, res) => {
    res.render('index');
});

// Handle form submission
app.post('/chat', (req, res) => {
    const userInput = req.body.userInput;

    // Spawn a Python process
    const pythonProcess = spawn('python', ['chatbot.py', userInput]);

    pythonProcess.stdout.on('data', (data) => {
        const response = JSON.parse(data);
        res.send(response.response);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
