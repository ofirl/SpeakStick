import { useQueryClient } from "@tanstack/react-query";
import { UseCreateMutationWrapperOptions, UseCreateQueryWrapperOptions, axiosClient, useCreateMutation, useCreateQuery } from "./helpers";

type Config = {
  key: string,
  value: string,
  description: string,
  default_value: string
}

export const DEVELOPMENT_BUILDS_CONFIG = "ENABLE_DEVELOPMENT_BUILDS"
export const AUTOMATIC_UPDATES_CONFIG = "ENBALE_AUTOMATIC_UPDATES"
export const LOGS_API_KEY_CONFIG = "LOGS_API_KEY"
export const DEVICE_NAME_CONFIG = "DEVICE_NAME"
export const LOGGING_LEVEL_CONFIG = "LOGGING_LEVEL"
export const LOGS_HANDLER_LOGGING_LEVEL_CONFIG = "LOGS_HANDLER_LOGGING_LEVEL"

export const useGetConfigs = <T extends object | boolean = Config[]>(advanced: boolean = false, options?: UseCreateQueryWrapperOptions<Config[], T>) => {
  return useCreateQuery({
    queryKey: ['configs', advanced.toString()],
    queryFn: () => axiosClient.get("/configs", { params: { advanced: advanced ? 1 : 0 } }).then(value => value.data as Config[]),
    errorMsg: "Error getting configs",
    ...options
  })
};

type updateConfigParams = { key: string, value: string };
export const useUpdateConfig = ({ onSuccess, ...options }: UseCreateMutationWrapperOptions<boolean, updateConfigParams> = {}) => {
  const queryClient = useQueryClient();
  return useCreateMutation({
    mutationFn: (params: updateConfigParams) =>
      axiosClient.post("/configs", params).then(value => value.status === 200),
    successMsg: "Config updated",
    errorMsg: "Error updating config",
    invalidateQueries: ["configs"],
    onSuccess: (data, variables, context) => {
      if (variables.key === DEVELOPMENT_BUILDS_CONFIG)
        queryClient.invalidateQueries({ queryKey: ["versions"] });

      onSuccess?.(data, variables, context)
    },
    ...options,
  }
  )
};