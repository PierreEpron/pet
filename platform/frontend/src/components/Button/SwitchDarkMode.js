import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";
import React, { useState } from "react";
import Switch from "@material-ui/core/Switch";
import useMediaQuery from '@material-ui/core/useMediaQuery';
import CssBaseline from '@material-ui/core/CssBaseline';
import deepPurple from '@material-ui/core/colors/deepPurple';


export default function DarkMode() {
  const [darkState, setDarkState] = useState(false);
  const palletType = darkState ? "dark" : "light";
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const darkTheme = React.useMemo(
    () =>
      createMuiTheme({
        palette: {
          type: prefersDarkMode ? 'dark' : 'light',
            primary: deepPurple,
            secondary: deepPurple,
        },
      }),
    [prefersDarkMode],
    );
  const handleThemeChange = () => {
    setDarkState(!darkState);
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <Switch checked={darkState} onChange={handleThemeChange} />
    </ThemeProvider>
  );
}