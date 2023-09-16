import { ThemeProvider, createTheme, responsiveFontSizes } from "@mui/material";
import { PropsWithChildren } from "react";

let theme = createTheme();
theme = responsiveFontSizes(theme);

// theme.typography = {
//     ...theme.typography,
//     body2: {
//         ...theme.typography.body2,
//         [theme.breakpoints.down('md')]: {
//             fontSize: "0.7rem",
//         },
//     },
//     caption: {
//         ...theme.typography.caption,
//         [theme.breakpoints.down('md')]: {
//             fontSize: "0.5rem",
//         },
//     }
// }

// theme = createTheme({
//     ...theme,
//     typography: {
//         ...theme.typography,
//         [theme.breakpoints.down('md')]: {
//             backgroundColor: theme.palette.secondary.main,
//         },
//         fontSize: 10,
//     },
//     palette: {
//         //   primary: {
//         //     main: red[500],
//         //   },
//     },
// });


type MuiThemeProviderProps = PropsWithChildren
export const MuiThemeProvider = ({ children }: MuiThemeProviderProps) => {
    return <ThemeProvider theme={theme}>
        {children}
    </ThemeProvider>;
}