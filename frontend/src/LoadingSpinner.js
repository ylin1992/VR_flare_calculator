import React from 'react'
import Loader from "react-loader-spinner";

function LoadingSpinner() {
    return (
        <div>
            {/*<i className="fa fa-spinner fa-spin" /> Loading...*/}
            <Loader
                type="ThreeDots"
                color="#DBE6FD"
                height={300}
                width={300}
            />
        </div>

    )
}

export default LoadingSpinner
