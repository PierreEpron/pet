import axios from 'axios';

const REACT_APP_API_URL = "http://localhost:8000/api"

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