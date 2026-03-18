import express from "express";
import { exec } from "child_process";
import fs from "fs";

const app = express();
app.use(express.json({ limit: "50mb" }));

app.post("/dump", (req, res) => {
    const { code } = req.body;

    if (!code) return res.status(400).json({ error: "No code provided" });

    fs.writeFileSync("input.lua", code);

    exec("python3 controller_main.py input.lua --mode=full --output=analysis.json", (err, stdout) => {
        if (err) return res.status(500).json({ error: err.toString() });

        const preview = stdout.slice(-1800);

        const json = fs.existsSync("analysis.json")
            ? fs.readFileSync("analysis.json", "utf8")
            : "{}";

        res.json({
            preview,
            analysis: JSON.parse(json)
        });
    });
});

app.listen(3000, () => console.log("Render dump API running on port 3000"));
