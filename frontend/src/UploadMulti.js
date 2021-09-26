import React, {useState} from 'react'
import axios from 'axios';
function UploadMulti() {

    const [images, setImages] = useState([]);
    const [formData, setFormData] = useState(new FormData());
    const [result, setResult] = useState(null)
    function handleOnChange(e){
        setResult(null);
        console.log(e.target.files);
        console.log(e.target.files[0]);
        const tempImagesArr = [];
        const tempFormData = new FormData();
        for (let i = 0; i < 3; i++) {
            tempImagesArr.push(URL.createObjectURL(e.target.files[i]))
            tempFormData.append(`image`,e.target.files[i])
            console.log(tempImagesArr)
        }
        setImages(tempImagesArr);
        setFormData(tempFormData);
        console.log("Form Data");
        console.log(formData);
    }

    function handleCalculateOnClick(){
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
        })
        .catch(err => {
            console.log(err);
        })
    }

    function renderImages(){
        return (
            <div>
                <img src={images[0]} alt="" />
                <img src={images[1]} alt="" />
                <img src={images[2]} alt="" />
            </div>
        )
    }

    function renderButton() {
        return (
            <div>
                <button onClick={handleCalculateOnClick}>
                    Calculate
                </button>
            </div>
        )
    }

    function renderResult() {
        return (
            <div>
                <h2>Result: {result.result}</h2>
                <img src={result.result_image} alt="" /> 
            </div>
        )
    }

    return (
        <div>
            <input type="file" name="images" onChange={handleOnChange} multiple />
        
            {(images.length > 0 && result === null) && renderImages()}
            {(images.length > 0 && result === null) && renderButton()}
            {result !== null && renderResult()}
        </div>
    )
}

export default UploadMulti
