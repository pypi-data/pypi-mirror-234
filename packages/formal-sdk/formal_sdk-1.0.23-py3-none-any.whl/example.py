import os
import formal_sdk

if __name__ == '__main__':
    # Import data types for the requests
    # example: from formal_sdk.gen.admin.v1.client_name_pb2 import methodNameRequest
    # for NativeUserClient it will be native_user_pb2
    # the client_name_pb2 contains the request and response class
    # for example: CreateNativeUserRequest for CreateNativeUser method
    from formal_sdk.gen.admin.v1.native_user_pb2 import CreateNativeUserRequest

    # Initialize formal client
    api_key = os.environ.get('API_KEY')
    formal_client = formal_sdk.Client(api_key)

    # Create Native Role
    data_store_id = ""
    native_user_id = ""
    native_user_secret = ""
    use_as_default = False

    createdRole = formal_client.NativeUserClient.CreateNativeUser(CreateNativeUserRequest(
        data_store_id=data_store_id,
        native_user_id=native_user_id,
        native_user_secret=native_user_secret,
        use_as_default=use_as_default)
        )

    # Get Native Role
    from formal_sdk.gen.admin.v1.native_user_pb2 import GetNativeUserRequest
    # NOTE: inline import intended for examples to see the import pattern, follow PEP 8 recommendation to import on your code

    previousRole = formal_client.NativeUserClient.GetNativeUser(
        GetNativeUserRequest(data_store_id=data_store_id, native_user_id=native_user_id)
        )

    print(f'data_store_id: {previousRole.native_user.datastore_id}')
    print(f'native_role_id: {previousRole.native_user.native_user_id}')
    print(f'native_role_secret: {previousRole.native_user.native_user_secret}')
    print(f'use_as_default: {previousRole.native_user.use_as_default}')

    # Get sidecar tls certificate and private key
    from formal_sdk.gen.admin.v1.sidecar_pb2 import GetSidecarTlsCertificateByIdRequest 
    # NOTE: inline import intended for examples to see the import pattern, follow PEP 8 recommendation to import on your code

    sidecar_id = ""
    secret = formal_client.SidecarClient.GetSidecarTlsCertificateById(GetSidecarTlsCertificateByIdRequest(id=sidecar_id))
    print(f'secret: {secret.secret}')

    # Empty request parameter example
    from formal_sdk.gen.admin.v1.identities_pb2 import GetUsersRequest
    # NOTE: inline import intended for examples to see the import pattern, follow PEP 8 recommendation to import on your code

    user_client = formal_client.UserClient
    print(user_client.GetUsers(GetUsersRequest())) # empty param need to pass the request object without any param
    print(user_client.GetUsers(GetUsersRequest()).users[0].id)
