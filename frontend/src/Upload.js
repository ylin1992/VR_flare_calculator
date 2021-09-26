import React, {useState, useEffect} from 'react'
import axios from 'axios'
import FormData from 'form-data'
function Upload() {

    const [image, setImage] = useState({});

    function handleOnClick(target) {
        console.log(target.value);
    }

    useEffect( () => {
        var formData = new FormData();
        var imagefile = document.querySelector('.file');
        formData.append("image", imagefile.files[0]);

        axios.post("http://localhost:5000/upload", formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
              }          
        })
        .then( response => {
            setImage(response)
            console.log(response)
        })
    }, [])

    return (
        <div>
            
            <form action="http://localhost:5000/upload" method="post" encType="multipart/form-data" >
                <Browse img_filed="image_w_1x" />
                <Browse img_filed="image_b_1x" />
                <Browse img_filed="image_w_8x" />
            </form>

                
            
            {/*<Browse handleOnClick={handleOnClick} img_field="image_w_1x" />*/}
        </div>
    )
}

export default Upload



function Browse (props){

    function handleOnClick(event){
        props.handleOnClick(event.target)
        console.log(event.target)
    }

    return (
        <div>
            <label>
                Browse 
                <input className="file" type="file" name="image" />
            </label>
            <input onClick={handleOnClick} type="submit" name="img_name" value={props.img_field}/>
        </div>
    )
}

function Image (props) {
    return (
        <div>
            {(props.image) ? 
            <img src={props.image} alt=""/>
            :
            null
            }
        </div>
    )
}