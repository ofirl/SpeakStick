import { useQueryClient } from "@tanstack/react-query";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useUpgradeStatus } from "../api/versions";

export const useWaitForUpgrade = (timeout: number = 60000) => {
    const [waitForUpgrade, setWaitForUpgrade] = useState(false);
    const timeoutRef = useRef<number>();
    const queryClient = useQueryClient()

    const { data: isUpgrading } = useUpgradeStatus({
        enabled: waitForUpgrade,
        refetchInterval: 10000,
    });

    const stopWaitingForUpgrade = useCallback(() => {
        setWaitForUpgrade(false)
        clearTimeout(timeoutRef.current)
    }, [])

    useEffect(() => {
        if (waitForUpgrade && !isUpgrading) {
            stopWaitingForUpgrade()
            setTimeout(() => {
                window.location.reload()
            }, 3000);
        }
    }, [waitForUpgrade, isUpgrading, stopWaitingForUpgrade])

    const startWaitingForUpgrade = useCallback((timeoutOverride: number = timeout) => {
        setTimeout(() => {
            setWaitForUpgrade(true)
        }, 1000);

        timeoutRef.current = setTimeout(() => {
            setWaitForUpgrade(false)
            queryClient.setQueryData(["upgrade", "status"], false)
        }, timeoutOverride);
    }, [queryClient, timeout])

    return useMemo(() => ({ startWaitingForUpgrade, isUpgrading, stopWaitingForUpgrade }), [isUpgrading, startWaitingForUpgrade, stopWaitingForUpgrade])
};