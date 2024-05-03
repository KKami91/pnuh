// 'use client';
// import { useState } from 'react';
// import axios from 'axios';
// import Image from 'next/image';

// export default function StressPlotPage() {
//   const [date, setDate] = useState('');
//   const [plotData, setPlotData] = useState('');

//   const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
//     e.preventDefault();
  
//     try {
//       const response = await axios.post('/realtime_test', { date });
//       setPlotData(response.data.plotData);
//     } catch (error) {
//       console.error('Error:', error);
//     }
//   };

//   return (
//     <div className="container mx-auto">
//       <h1 className="text-2xl font-bold mb-4">Stress Plot</h1>
//       <form onSubmit={handleSubmit}>
//         <input
//           type="date"
//           value={date}
//           onChange={(e) => setDate(e.target.value)}
//           className="border border-gray-300 rounded px-2 py-1 mb-4"
//         />
//         <button type="submit" className="bg-blue-500 text-white rounded px-4 py-2">
//           Submit
//         </button>
//       </form>
//       {plotData && (
//         <Image
//           src={`data:image/png;base64,${plotData}`}
//           alt="Stress Plot"
//           width={500}
//           height={300}
//         />
//       )}
//     </div>
//   );
// }

'use client';
import { useState } from 'react';
import axios from 'axios';

export default function RealtimeTest() {
  const [output, setOutput] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
  
    try {
      const response = await axios.post('/api/realtime_test', {});
      setOutput(response.data.output);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
  return (
    <div>
      <h1>Realtime Test</h1>
     
      <form onSubmit={handleSubmit}>
        <button type="submit">Execute Command</button>
      </form>
      <pre>{output}</pre>
    </div>
  );
}