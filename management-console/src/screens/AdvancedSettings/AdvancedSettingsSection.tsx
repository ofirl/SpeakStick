import { CSSProperties, ReactNode } from "react";
import { Accordion, AccordionDetails, AccordionSummary, Typography } from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

type AdvancedSettingsSectionProps = {
  title: string
  children: ReactNode
  detailsStyle?: CSSProperties
}
export const AdvancedSettingsSection = ({ children, title, detailsStyle }: AdvancedSettingsSectionProps) => {
  return (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography>{title}</Typography>
      </AccordionSummary>
      <AccordionDetails style={{ display: "flex", flexDirection: "column", gap: "1rem", ...detailsStyle }}>
        {children}
      </AccordionDetails>
    </Accordion>
  )
}