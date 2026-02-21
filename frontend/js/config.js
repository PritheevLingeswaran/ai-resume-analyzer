// Frontend Config: choose backend base URL and enable mocks
(function(){
  const params = new URLSearchParams(window.location.search);
  const qApi = params.get('api');
  const qMocks = params.get('mocks');
  if(qApi) localStorage.setItem('SRA_BASE_URL', qApi);
  if(qMocks !== null) localStorage.setItem('SRA_USE_MOCKS', qMocks === '1' || qMocks === 'true');

  window.SRA_CONFIG = {
    BASE_URL: localStorage.getItem('SRA_BASE_URL') || (location.hostname === 'localhost' ? 'http://localhost:8080' : `${location.origin}`),
    USE_MOCKS: (localStorage.getItem('SRA_USE_MOCKS') === 'true')
  };
  console.debug('[SRA] CONFIG', window.SRA_CONFIG);
})();
