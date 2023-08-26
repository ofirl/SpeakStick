import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';

type DeleteWordModalProps = {
    open: boolean,
    word: string,
    positions: string[]
    onApprove: () => void,
    onDecline: () => void
}
export const DeleteWordModal = ({ open = false, onApprove = () => { }, onDecline = () => { }, word = "", positions = [] }: DeleteWordModalProps) => {
    return (
        <Dialog
            open={open}
            onClose={onDecline}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
        >
            <DialogTitle id="alert-dialog-title">
                {`Delete ${word}?`}
            </DialogTitle>
            <DialogContent>
                <DialogContentText id="alert-dialog-description">
                    Deleting this word means deleting all the positions that's using it, those positions are:
                    {positions.join(", ")}
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button color="info" onClick={onDecline}>Disagree</Button>
                <Button color="warning" onClick={onApprove} autoFocus>
                    Agree
                </Button>
            </DialogActions>
        </Dialog>
    )
};