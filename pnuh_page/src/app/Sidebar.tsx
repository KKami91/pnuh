import Link from 'next/link';

const Sidebar = () => {
  return (
    <div className="h-screen w-64 bg-gray-800 text-white p-4">
      <nav>
        <ul>
          <li>
            <Link href="/">Home</Link>
          </li>
          <li>
            <Link href="/test">Test</Link>
          </li>
          <li>
            <Link href="/raw">Raw Data</Link>
          </li>
          <li>
            <Link href="/stress">Stress Score</Link>
          </li>
          <li>
            <Link href="/realtime_test">Realtime</Link>
          </li>
          {/* 추가적인 메뉴 항목을 여기에 추가할 수 있습니다. */}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;