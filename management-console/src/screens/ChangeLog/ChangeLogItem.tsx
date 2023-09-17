import { ChangeLog } from "../../api/versions";

import ReactMarkdown from 'markdown-to-jsx';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import { ComponentProps } from "react";
import { Accordion, AccordionDetails, AccordionSummary } from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const options = {
    overrides: {
        h1: {
            component: Typography,
            props: {
                gutterBottom: true,
                variant: 'h4',
            },
        },
        h2: {
            component: Typography,
            props: { gutterBottom: true, variant: 'h6' },
        },
        h3: {
            component: Typography,
            props: { gutterBottom: true, variant: 'subtitle1' },
        },
        h4: {
            component: Typography,
            props: {
                gutterBottom: true,
                variant: 'caption',
                paragraph: true,
            },
        },
        p: {
            component: Typography,
            props: { paragraph: true },
        },
        a: { component: Link },
        li: {
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            component: (props: any) => (
                <Box component="li" sx={{ mt: 1 }}>
                    <Typography component="span" {...props} />
                </Box>
            ),
        },
    },
};

const Markdown = (props: ComponentProps<typeof ReactMarkdown>) => {
    return <ReactMarkdown options={options} {...props} />;
}

type ChangeLogItemProps = ChangeLog & {
    defaultExpanded?: boolean
};
export const ChangeLogItem = ({ title, description, defaultExpanded }: ChangeLogItemProps) => {
    return (
        <Accordion defaultExpanded={defaultExpanded}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>{title}</Typography>
            </AccordionSummary>
            <AccordionDetails>
                <Markdown options={options}>
                    {`${description}`}
                </Markdown>
            </AccordionDetails>
        </Accordion>
    );
};