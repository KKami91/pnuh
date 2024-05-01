///import hrv from "C:\Users\AIA01\Desktop\project\PNUh\pnuh_page\public\hrv_json\health_data_HeartRateRecord_20240416_154527.json";

///console.log(hrv);

// var jss = {
//   id : 'sss',
//   pwd : '1234'
// };

// var keys = Object.keys(jss);
// for (var i=0; i<keys.length; i++) {
//   var key = keys[i]
//   console.log("key : " + key + ", value : " + jss.id )
// }

const TestPage = () => {
    return (
      <div className="p-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to Raw Page</h1>
        <p className="text-lg mb-8">This is a sample page created using Next.js, TypeScript, and Tailwind CSS.</p>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Click me
        </button>
      </div>
    );
  };
  
  export default TestPage;