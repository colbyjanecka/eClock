import React, { useState } from "react";
import { TypeAnimation } from 'react-type-animation';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import Button from "@mui/material/Button";
import { createTheme, ThemeProvider } from '@mui/material/styles'


function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const theme = createTheme({
    palette: {
      primary: {
        main: '#52B788',
        // light: will be calculated from palette.primary.main,
        // dark: will be calculated from palette.primary.main,
        // contrastText: will be calculated to contrast with palette.primary.main
      },
      secondary: {
        main: '#2D6A4F',
        light: '#95D5B2',
        // dark: will be calculated from palette.secondary.main,
        contrastText: '#FF9671',
      },
    },
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("text", text);
    if (file) formData.append("photo", file);

    try {
      const res = await fetch("/api/upload", { method: "POST", body: formData });
      if (!res.ok) {
        const txt = await res.text();
        setStatus(`HTTP ${res.status}: ${txt}`);
        return;
      }
      const data = await res.json();
      setStatus("Upload ok");
    } catch (err) {
      console.error("Full error:", err);
      console.error("Stack:", err.stack);
      setStatus(`Network error: ${err.message}`);
    }
  };
  return (
    <ThemeProvider theme={theme}>
    <Stack alignItems="center" justifyContent="center" spacing={10} sx={{ 
      minHeight: "auto",  // fill viewport
      maxHeight: "100vh",  // fill viewport
      width: "100%",
      p: 1,
      mx: 0,
    }}>
      <TypeAnimation
        sequence={[
          'hey ann wei...',
          2000, // Waits 2s
          'hey annie...', // Types 'One'
          1000, // Waits 1s
          'hey minty...', 
          2000, // Waits 2s
          'hey ann...', 
          2000, // Waits 2s
          'hey pretty girl...',
          2000, // Waits 2s
          'hey @nowei...',
          2000, // Waits 2s
          'hey ...',
          2000, // Waits 2s
          () => {
            console.log('Sequence completed');
          },
        ]}
        speed={2}
        wrapper="span"
        cursor={true}
        repeat={Infinity}
        style={{ fontSize: '12vw', fontOpticalSizing: 'auto'}}
      />
      <Paper square={false} elevation={5} sx={{ 
        p: "2vw", 
        m: "5vw", 
        minWidth: ".9",
        width: "98vw",  // responsive
        maxWidth: ".8",
      }} align="center">
          {status && <div>{status}</div>}
            <Stack component="form" onSubmit={handleSubmit} alignItems="center" spacing={5} sx={{
                  p: "2vh",
                }}>
              <TextField
                value={text} sx={{
                  width: "100%",
                  // Target the input element inside TextField
                  '& .MuiInputBase-input': {
                  fontSize: '4vw', // Your desired font size
                  p: '2vw'
                },
                }}
                id="filled-multiline-static" 
                label="Message" 
                multiline
                fullWidth
                rows={5} 
                color="secondary" focused
                onChange={(e) => setText(e.target.value)}/>
              <Stack direction="row" alignItems="center" spacing={4} sx={{pb: "20px"}}>
                <Button variant="contained" component="label" color="primary" size="large">
                  Upload Image
                  <input hidden accept="image/*" type="file"  onChange={(e) => setFile(e.target.files[0])}/>
                </Button>
                <Button type="submit" color="primary" size="large">Submit</Button>
              </Stack>
            </Stack>
            {file && <div>{file.name}</div>}
          </Paper>
    </Stack>
    </ThemeProvider>
  );
}

export default App;
