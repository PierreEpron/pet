import axios from 'axios';
import {REACT_APP_API_URL} from './apiConfig'

function upload(fileData) {
    axios.post(REACT_APP_API_URL + "/upload/", fileData)
    .then(function (response) {
        console.log(response)
    })
    .catch(function (error) {
        console.log(error)
    })

}

export {upload}