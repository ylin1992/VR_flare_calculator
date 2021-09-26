import React, {useState} from 'react'
import axios from 'axios';
import {Container, Col, Row} from "react-bootstrap"
import LoadingSpinner from './LoadingSpinner';
function UploadMulti() {


    const [isLoading, setIsLoading] = useState(false);
    const [images, setImages] = useState([]);
    const [formData, setFormData] = useState(new FormData());
    const [result, setResult] = useState(null)

    function handleOnChange(e){
        setResult(null);
        const tempImagesArr = [];
        const tempFormData = new FormData();
        for (let i = 0; i < 3; i++) {
            tempImagesArr.push(URL.createObjectURL(e.target.files[i]))
            tempFormData.append(`image`,e.target.files[i])
        }
        setImages(tempImagesArr);
        setFormData(tempFormData);
        setResult(null);
    }

    function handleCalculateOnClick(){
        setIsLoading(true);
        axios.post("http://localhost:5000/upload-files", 
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
        .then(response => {
            console.log(response);
            setResult(response.data);
            setIsLoading(false);
            setImages([]);
        })
        .catch(err => {
            console.log(err);
        })
    }


      
    function handleSampleOnClick() {
        axios.get("http://localhost:5000/load-sample")
        .then( response => {
            console.log(response.data)
            setResult(null);
            const tempImagesArr = [];
            const tempFormData = new FormData();

            //console.log(typeof(response.data[0].image))
            //console.log(response.data[0].image.split(",")[1].trim())
            for (let i = 0; i < 3; i++) {
                tempImagesArr.push(response.data[i].image)
                console.log(response.data[i].image)
                //tempFormData.append(`image`,response.data[i])
            }
            setImages(tempImagesArr);
            //setFormData(tempFormData);
            setResult(null);
        })
        .catch( err => {
            console.log(err);
        })
    }

    function renderImages(){
        return (
            <div className="images-container">
            <Container fluid>
                <Row >
                <Col sm={6} md lg={4}>
                    <img className="images__upload" src={images[0]} alt="" />
                </Col>
                <Col sm={6} md lg={4}>
                    <img className="images__upload" src={images[1]} alt="" />
                </Col>
                <Col sm={6} md lg={4}>
                    <img className="images__upload" src={images[2]} alt="" />
                </Col>
                </Row>
            </Container>
            </div>
        )
    }

    function renderButton() {
        return (
            <div>
                <button onClick={handleCalculateOnClick} className="btn btn-primary">
                    Calculate
                </button>
            </div>
        )
    }

    function renderResult() {
        return (
            <div id="result">
                <h2>Result: {result.result}</h2>
                <img className="images__result" src={result.result_image} alt="" /> 
            </div>
        )
    }

    return (
        <div id="images">
            {!isLoading && 
                <div>
                    <label className="btn btn-primary upload-btn">
                        Upload 3 images
                        <input type="file" name="images" onChange={handleOnChange} multiple hidden/>
                    </label>
                    <button className="btn btn-primary upload-btn" onClick={handleSampleOnClick}>Load Sample Images</button>
                </div>
            }
            {isLoading && <LoadingSpinner />}
            {(!isLoading && images.length > 0 && result === null) && renderImages()}
            {(!isLoading && images.length > 0 && result === null) && renderButton()}
            {result !== null && renderResult()}
        </div>
    )
}

export default UploadMulti
