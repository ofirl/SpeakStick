import { useRef, useCallback } from "react"

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const useDebounce = <T extends any[]>(func: (...arg0: T) => void, delay = 500) => {
    const timeout = useRef<number>(0)

    return useCallback((...args: T) => {
        if (timeout.current)
            clearTimeout(timeout.current);

        timeout.current = setTimeout(() => {
            func(...args)
        }, delay);
    }, [func, delay])
};