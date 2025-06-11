const FileUpload = () => {
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        // Handle file upload logic here
        console.log(file);
    };

    return (
        <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="mb-4"
        />
    );
};

export default FileUpload;
