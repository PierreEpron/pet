import React from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from '@material-ui/core/Typography';
import {makeStyles} from '@material-ui/core/styles';
import {green} from '@material-ui/core/colors';
import {getContents} from "../services/content.service"

const useStyles = makeStyles((theme) => ({

}));

export default function ApplyQueueFeedBack(props) {
    const classes = useStyles();
    
    const [queueCount, setQueueCount] = React.useState(localStorage.getItem('queueCount'));

    const handleApplySuccess = (data) => {
        const c = data.queue.count;
        localStorage.setItem('queueCount', c);
        setQueueCount(c);
    }

    React.useEffect(() => {
        if (queueCount >= 0)
            getContents("/apply-queue/", {}, handleApplySuccess)
    }, [queueCount])

    if (queueCount === null || queueCount <= 0)
        return (<div></div>)

    return (
        <div>
           <Typography component="span">
               Restant : {queueCount}
            </Typography>
        </div>
    )
}

