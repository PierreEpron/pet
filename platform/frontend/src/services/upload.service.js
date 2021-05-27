import axios from 'axios';
import {onBadAuth} from './auth.service'
import {REACT_APP_API_URL} from './apiConfig'
import {getHeader} from './apiHelpers'

function upload(fileData, onSucces) {
    axios.post(REACT_APP_API_URL + "/upload/", fileData, {headers: getHeader(true)})
    .then(function (response) {
        onSucces()
    })
    .catch(function (error) {
        switch (error.response.status) {
            case 401:
                onBadAuth()
                break
            default:
                console.log(error)
                break             
        } 
    })
}

export {upload}