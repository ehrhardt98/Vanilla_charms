import openstack

def create_connection(auth_url, region, project_name, username, password):

    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
        region_name=region,
        app_name='examples',
        app_version='1.0',
    )

# Initialize and turn on debug logging
openstack.enable_logging(debug=True)

# Initialize connection
# Cloud configs are read with openstack.config
conn = create_connection("http://192.168.1.227:5000/v3", "RegionOne", "admin", "jorgg", "cloudr")

image = conn.compute.find_image("bionic")
flavor = conn.compute.find_flavor("m1.small")
network = conn.network.find_network("jorgg-net")
keypair = conn.compute.find_keypair("maas")

server = conn.compute.create_server(
    name="jorgg_instance1", image_id=image.id, flavor_id=flavor.id,
    networks=[{"uuid": network.id}], key_name=keypair.id)

server = conn.compute.wait_for_server(server)

del_server = conn.compute.find_server("jorgg_instance1")

conn.compute.delete_server(del_server)
