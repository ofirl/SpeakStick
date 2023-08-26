import { useRef, useState } from "react";
import Paper from "@mui/material/Paper";
import IconButton from "@mui/material/IconButton";
import InputBase from "@mui/material/InputBase";
import Divider from "@mui/material/Divider";
import SaveIcon from '@mui/icons-material/Save';

import CancelIcon from '@mui/icons-material/Cancel';
import EditIcon from '@mui/icons-material/Edit';

type ValueCellProps = {
    value: string
    onEdit: (value: string) => void
}
export const ValueCell = ({ value, onEdit }: ValueCellProps) => {
    const [editMode, setEditMode] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    const toggleEditMode = () => setEditMode(prev => !prev)

    return !editMode ? (
        <>
            {value}
            <IconButton type="button" sx={{ p: '10px' }} aria-label="edit" onClick={toggleEditMode}>
                <EditIcon />
            </IconButton>
        </>
    ) : (
        <Paper
            component="form"
            sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: "15rem" }}
        >
            <InputBase
                sx={{ ml: 1, flex: 1 }}
                defaultValue={value}
                inputRef={inputRef}
            />
            <IconButton type="button" sx={{ p: '10px' }} aria-label="search" onClick={() => inputRef.current && onEdit(inputRef.current.value)}>
                <SaveIcon />
            </IconButton>
            <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
            <IconButton color="primary" sx={{ p: '10px' }} aria-label="directions" onClick={toggleEditMode}>
                <CancelIcon />
            </IconButton>
        </Paper>
    )
};