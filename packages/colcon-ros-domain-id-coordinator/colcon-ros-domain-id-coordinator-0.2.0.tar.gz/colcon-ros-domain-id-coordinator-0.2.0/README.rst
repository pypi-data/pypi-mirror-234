colcon-ros-domain-id-coordinator
================================

An extension for `colcon-core <https://github.com/colcon/colcon-core>`_ to coordinate different DDS `domain IDs <https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Domain-ID.html>`_ for concurrently running tasks.

The current implementation of this package cycles through all of the non-default ROS 2 domain IDs that should be available on a platform given that it has no special network configurations.
It does not track which task uses the domain IDs and therefore does not eliminate the possibility of a collision, but drastically reduces the likelihood that two tasks end up using the same domain ID.
