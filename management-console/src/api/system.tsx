import { UseQueryOptions, useMutation, useQuery } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

import { toast } from "react-toastify";

export const useRestartStickController = () => {
  return useMutation(() =>
    axios.get(baseUrl + "/restart/stick-controller").then(value => value.status === 200),
    {
      onSuccess: () => {
        toast.success("Stick controller restarted")
      },
      onError: () => {
        toast.error("Error restarting stick controller")
      }
    }
  )
};

export const useResetToFactorySettings = () => {
  return useMutation(() =>
    axios.get(baseUrl + "/reset_factory_settings").then(value => value.status === 200),
    {
      onSuccess: () => {
        toast.success("Application is resetting to factory settings, this might take a few seconds")
      },
      onError: () => {
        toast.error("Error resetting application to factory settings")
      }
    }
  )
};

export type BatteryPercentResult = { percent: number, isCharging: boolean };
export const useGetBatteryPercent = (options: UseQueryOptions<BatteryPercentResult, unknown, BatteryPercentResult, string[]> = {}) => {
  return useQuery(
    ['battery', 'percent'],
    () => axios.get(baseUrl + "/battery/percent").then(value => value.data as BatteryPercentResult),
    {
      refetchInterval: 30000,
      ...options
    },
  )
};

export const servicesOptions = ["speakstick", "speakstick-management-server"] as const;
export type Services = typeof servicesOptions[number];
export const useGetServiceLogs = (service: Services, options: UseQueryOptions<string, unknown, string, string[]> = {}) => {
  return useQuery(
    ['logs', service],
    () => axios.get(baseUrl + `/logs/${service}`).then(value => value.data as string),
    {
      refetchInterval: 10000,
      ...options
    },
  )
};