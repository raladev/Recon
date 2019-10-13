const b64file = 'file in base 64'
const contentType - 'content type of file'

const b64toBlob = (b64Data, contentType='', sliceSize=512) => {
  	const byteCharacters = atob(b64Data);
  	const byteArrays = [];

  	for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    	const slice = byteCharacters.slice(offset, offset + sliceSize);

    	const byteNumbers = new Array(slice.length);
    	for (let i = 0; i < slice.length; i++) {
      		byteNumbers[i] = slice.charCodeAt(i);
    		}

    	const byteArray = new Uint8Array(byteNumbers);
    	byteArrays.push(byteArray);
  	}

  	const blob = new Blob(byteArrays, {type: contentType});
  	return blob;
	}

function send_file()
{
	var uri ="endpint for file uploading";
	xhr = new XMLHttpRequest();
	xhr.open("POST", uri, true);

    const blob = b64toBlob(b64file, fileContentType);

    formData = new FormData();
    formData.append("VarName", blob, 'FileName')

	xhr.send(formData);
}
send_file();
