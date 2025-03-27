let posterid = "Poster1";

async function getRootPage(){
  window.location.replace(window.location.origin);
}

async function getPage(page){
  window.location.replace(window.location.origin+'/'+page);
}

async function fetchData(url) {
    try {
    //url="localhost/80/" + url
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json(); // Parse JSON from the response
      console.log('Data received:', data); // Handle the retrieved data
      return await data; // Return the data if needed
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error); // Handle errors
      throw error; // Propagate the error if needed
    }
}