import { useState } from "react";
import IconButton from "@mui/material/IconButton";
import { CircularProgress } from "@mui/material";
import RestoreIcon from '@mui/icons-material/Restore';

type DefaultValueCellProps = {
    value: string
    onRestore: () => Promise<boolean>
}

export const DefaultValueCell = ({ value, onRestore }: DefaultValueCellProps) => {
    const [isLoading, setIsLoading] = useState(false);

    const onSave = () => {
        setIsLoading(true);

        onRestore().then(() => {
            setIsLoading(false)
        })
    }

    return (
        <>
            {value}
            <IconButton type="button" sx={{ p: '10px' }} aria-label="edit" onClick={onSave}>
                {isLoading ? <CircularProgress /> : <RestoreIcon />}
            </IconButton>
        </>
    )
};