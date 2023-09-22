import { ThemeProvider, createTheme, responsiveFontSizes } from "@mui/material";
import { PropsWithChildren } from "react";

let theme = createTheme();
theme = responsiveFontSizes(theme);

type MuiThemeProviderProps = PropsWithChildren
export const MuiThemeProvider = ({ children }: MuiThemeProviderProps) => {
    return <ThemeProvider theme={theme}>
        {children}
    </ThemeProvider>;
}