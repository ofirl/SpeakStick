import './App.css'
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Settings } from './screens/settings/Settings';
import { Words } from './screens/words/Words';
import { TopBar } from './components/TopBar/TopBar';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

function App() {
    return (
        <>
            <QueryClientProvider client={queryClient}>
                <BrowserRouter basename="/">
                    <TopBar />
                    <Routes>
                        <Route path="/settings" Component={Settings} />
                        <Route path="/words" Component={Words} />
                    </Routes>
                </BrowserRouter>
            </QueryClientProvider>
        </>
    )
}

export default App
