import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const TemplatePage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const templates = [
    "https://lh3.googleusercontent.com/aida-public/AB6AXuBQXppkarvpy6MuP5vtvJOW6HO923zdc9LcFWceqLrZqTWbIUKcZGB27_NZJskPmQpDyX4Lx9JY3u7p7GjROT2mM6iavxY86JHhpJbVy0zkSc9qAlhUM4ZVz-Bx4CQb02wTSgxtkFi5Sn114cqjd0c2IymVxpDXm2GbecCWx0GJLPnp2faXcxHJK-fZCup_Xg35FDHVqtBvy0xXB1kq0LHca4FlqBOds05TYVeYYKW-Xv6JL-uglWotPW8-_MDLZiQeqoH4ad8FLScA",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuC3BZPG4liv7QNgdX0QHNIKK84Syk16ynsgJP8lFVqX5e1-xybVUnzZHYoL51I7buO6Uu-nEfnTlFP5_tziGSRTDcEbTh4L_kcusRnwyddxyT4zp9vzvMKiE8QHcqRJrDYyX-ywRmnFnjPxhJoUwZjoz5EVwrQ6dG_r-BJq96_lpvAgILXEYK25yV0eEBB4mN3tZHPIusQLJec4-Ah2MVY0eI5B6eZQmDh9xuFxbaWBoXd_g6GLbDGY79j6Z3vpGuv--a90ankUXWNF",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuAQQghANQeUpXdsXBqDLtnl7MyijxaDOn7owlpTs6oS0skbOViku9um3c9ib36eecJJqmc-KJxh1LLEfebJzKnTOINK441tiw_UPTv3NMmyjeiAUTtpitxp3PGUS74G29AgZOKYCWEKlF32j2A_wqQkfYtGEd8cJVnYkrSpXDVVqNnq_D_NSgrt88sydXYCterhg1UE3hzS9-S7RGP10yOj0A1xFHf8BM_vUYdQ1wmekcu65hNlzjbd0apO9gZ2J6W67stszQHwYZys",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuAIjIpv9sbtNRveNZItJtCYMQ3rVbIHKtOo1gRpY7pHf5Xt7-YdO9pL-5V4cA5UdCJhU4LgUxi61aCZjd7ES3QS3H7F6mSraQDeKE3QRwD5jgarkZ68NLZKNUoMhULNAz_VU_yllo8zsnDpK0BPL8SRHZD-I2Z-Kx00-EEHpyxiMo6aD3xUmfVXk3Zr0Aw_7cZvBar5B1bII-TDfUkPQGbDq4Qn_HRyVTWA5iE4-59hEMLUsAjVge2cMAJhRSGMUaRu64KgDEnFMk2p",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuCiq-rGfGOory9VlscSsmISXXL4ta_7_B204fWoAWMvqf_v48vU7CRXGDIBAa-8Qd3fANZiNFIYrvydCVk1cc6XXYA-E9Z84-fy1dmWPd1ecaw3beadQB66kntphB6uHHR2evMqPnbHTn1_-nCiQGtT8ES2vJazcEsXxN5FcqNETPbRYTEgAK74S0h-YbR9W7YoQLRgvDoLAY74m5KtuBCsb3GIavkjzjdpABa5GqL1UNsCnTPy8szreBCP90D5WHSBU1AgRSc-2YxB",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuAYmSrWdSAbxqHxisQjUADpnnyAZUD_6iIiC4v-7d_SX2d9s5IprvecVsyj852W3cK1W7k80DlfAZV_VC3DuWyXM0jz5zY3b-KZ0KXiAAXL4pm_YXsPyQ7uYtpzdbqhkH0gMTIp21VktolJ_fGrTGwkWIC9slfx3nUE_1IspjAXBveI1EzbrbLfiDH3_fdub-ifK8JcJQ6m--6nGDsMQn04lEyIvuk3imWh0o4lDy6-2WVX2JNstoJm3xGmdb9cLcUyavClgaA36o_H",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuAAOFKRVlEFMfHsuH_cLNZ6bw-D-Ny9mlcn2N3PiRztaRoQm4Qr9Fwc7XvW40mvMMqBF_zGXS-WVh3HGfj49-3fDT-NdP6AUDAG7Oab5qF_rBqOooy7J9u2Od2NU97e5mwrYfNXXT0UXBLYx6j8mvaVZ2JTd9Vz31iIizMvXMWHJ71phrTsONeVBty1JkwEdrdMvGbAlx26E6GztIu0C911H1Ztjx_Ol7WS_urjAzWK5Tgnhl_oxuuQkEoNYjeq3oqGCc-67aW7A2ZJ",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuCUlDteZ_mbRVNvQDLk5ftgA7Gtv5Zoz9qB_A3xMU6wj2z3WiVd0LlGcMR6d3TlGI-YDV9Jd820jVvx-dfWF4wxulTcQW9ZMpOKwdlNWojkn5yxLz0Tc4QnYkugTiiuQP6KhMOqTXNf7anENYpGIukn4TFECgB-iPPkVXEqlX1WLIEPdnzTlf_3F1yhPWBIleThEoP-_BChtTZO_uMfKWpvfvQEFtpfpDTCR1tsZ_vwLvFsuUtuEAt7hiZAtRgT094Dr--0mFSWud2E",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuAjwcvOG-a8CAxEFC0I0_Tzuuhr7E9OE765pts3v4Cj_vxhrLvj3JUDSEG2DiZkhrVw4CHdX2IwbFzvaQKUmciwfj7BitYiwpBpnuX0ok5zaFHSUNCEzFjpSn6On4Okq9I-5baUcuJBLpfviYLlm_MOFairGM0XcXd9b--1slxYjAgI4n6128tvOjDEkgsSxkYdfqrUJuScpA6OXyS6p-p2724wZiecOouSu6rvHvdqTRTT45zC0ffVoc8B2e9AY9uPkWSJQZaWnTpj",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuArfdwL_QcIJgfP3879_x8-HFwIBbnqYItrbbceZ4PuF3BirfYTOrB4rd8FGJXSc42vWPksl0LpAJfX1fKxRA9dOmRtvsMplsqz_YEDM-LF0vmJb_6Y9PfqiQOoiFKVL6S_VIGDE_jkwRbZKnxWlSvstgikwO0NuhXJBRnsXowimxVEp9gcplUt3Q3L4iaQAD1kFUccJsBzGXEsuAuM99yI0-VpUREHRKoT5HwJJJPfXjL00FCD0sPkzKkj-fGbMouitddXmeKy1szK",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuB9Jj6muHkeujvcuId-nkKb3dUUU46OaMHQx923MGklsx1527-fYBb5J0IARuLscbVpkoAzPfBjs_389gk3d7b8GQvOK6J10tdO5xvO-alBukKweDhaBakOIthXizL5S6xgImPDsOjV2Gnnuj6ZOnbOO13fz6J_PM6OZS0UH3q6RKduM7tFsf4PxcidmHJur9l2OAJRJ_qZ2lpgRoMKMBxROh0lHjPvgO-3V3xFGEBdheFRs8LsrLZsvbEK-5a_FWH5wIKDVaUnoJCe",
    "https://lh3.googleusercontent.com/aida-public/AB6AXuCZTc6PNws20TdBrnUQ1r9jI_4qRb9S1jcIXTktkmmsGAfj8xYez2CSs0kLzCojpefG8NX3XE--MTcyhVsiaTiYzc_EyholvWjJEKsewaNPs4fnVxPywiSLITBaH_X04caHDkkloGZvdiUXYGVt6PAilH4n5vq9uX1Sk_gwzDjReefghBnddKFEEdtP7P8fflQNeAqZiiw0Fqk5-60BvH3Yk8mXwT_fVq2ksCogzHoU8_p0aUeoyBbUOYEhxgzNQvHYVyvzjGdKnXsl"
  ];

  const handleTemplateClick = (templateUrl) => {
    navigate('/create', { state: { selectedTemplate: templateUrl } });
  };

  return (
    <div className="px-40 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
        <button
          className="mb-4 self-start text-white hover:underline text-sm"
          onClick={() => navigate('/')}
        >
          ← Back to Home
        </button>
        <div className="flex flex-wrap justify-between gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Choose a Template
          </p>
        </div>
        <div className="px-4 py-3">
          <label className="flex flex-col min-w-40 h-12 w-full">
            <div className="flex w-full flex-1 items-stretch rounded-xl h-full">
              <div className="text-[#9badc0] flex border-none bg-[#293542] items-center justify-center pl-4 rounded-l-xl border-r-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z"></path>
                </svg>
              </div>
              <input
                placeholder="Search templates"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border-none bg-[#293542] focus:border-none h-full placeholder:text-[#9badc0] px-4 rounded-l-none border-l-0 pl-2 text-base font-normal leading-normal"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </label>
        </div>
        <div className="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-4">
          {templates.map((template, index) => (
            <div key={index} className="flex flex-col gap-3">
              <div
                className="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-xl cursor-pointer hover:opacity-80 transition-opacity"
                style={{ backgroundImage: `url("${template}")` }}
                onClick={() => handleTemplateClick(template)}
              ></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TemplatePage; 