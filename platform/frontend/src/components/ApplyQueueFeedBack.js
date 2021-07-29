import React from 'react';
import Typography from '@material-ui/core/Typography';
import {getContents} from "../services/content.service"

export default function ApplyQueueFeedBack(props) {    
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
