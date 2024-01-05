exports.handler = async function(event, context) {
    const value = process.env.Weather_Api_Key;
  
    return {
        statusCode: 200,
        body: JSON.stringify({ message: value }),
    };  
};

