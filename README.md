# Iceoryx Performance Testing with Extended Payload Sizes

This README provides a step-by-step guide to clone the Iceoryx repository, modify the IcePerf example to support 8 MB and 16 MB payload sizes, and run performance benchmarks.

---

## Steps

### 1. Clone the Repository

Clone the Iceoryx repository:

```bash
git clone https://github.com/eclipse-iceoryx/iceoryx.git
cd iceoryx
```

---

### 2. Modify `iceperf_leader.cpp` for 8 MB and 16 MB Tests

Update the `iceperf_leader.cpp` file to include support for 8 MB and 16 MB payload sizes:

#### Patch Diff

Apply the following changes to `iceperf_leader.cpp`:

```diff
diff --git a/iceoryx_examples/iceperf/iceperf_leader.cpp b/iceoryx_examples/iceperf/iceperf_leader.cpp
index f95d1a5b7..82c847a81 100644
--- a/iceoryx_examples/iceperf/iceperf_leader.cpp
+++ b/iceoryx_examples/iceperf/iceperf_leader.cpp
@@ -92,7 +92,9 @@ void IcePerfLeader::doMeasurement(IcePerfBase& ipcTechnology) noexcept
                                             512 * IcePerfBase::ONE_KILOBYTE,
                                             1024 * IcePerfBase::ONE_KILOBYTE,
                                             2048 * IcePerfBase::ONE_KILOBYTE,
-                                             4096 * IcePerfBase::ONE_KILOBYTE};
+                                             4096 * IcePerfBase::ONE_KILOBYTE,
+                                             8192 * IcePerfBase::ONE_KILOBYTE,
+                                             16384 * IcePerfBase::ONE_KILOBYTE};
    std::cout << "Measurement for:";
    const char* separator = " ";
    for (const auto payloadSize : payloadSizes)
```

---

### 3. Build Iceoryx

Build the Iceoryx project and its examples:

```bash
./tools/iceoryx_build_test.sh build-all
```

---

### 4. Configure RouDi

1. Copy the example configuration file:

   ```bash
   cp build/install/prefix/etc/roudi_config_example.toml roudi_config.toml
   ```

2. Add the following memory pools to `roudi_config.toml`:

   ```toml
   # Memory pool for 8 MB chunks
   [[segment.mempool]]
   size = 8388608
   count = 5

   # Memory pool for 16 MB chunks
   [[segment.mempool]]
   size = 16777216
   count = 5

   # Memory pool for 32 MB chunks
   [[segment.mempool]]
   size = 33554432
   count = 5
   ```

---

### 5. Run the IcePerf Benchmark

1. Start RouDi with the updated configuration:

   ```bash
   build/install/prefix/bin/iox-roudi --config-file roudi_config.toml
   ```

2. In a new terminal, start the IcePerf follower:

   ```bash
   build/iceoryx_examples/iceperf/iceperf-bench-follower
   ```

3. In another terminal, start the IcePerf leader:

   ```bash
   build/iceoryx_examples/iceperf/iceperf-bench-leader
   ```

---

## Notes

* Ensure the memory pools in `roudi_config.toml` are sufficient for your tests.
* Modify payload sizes or memory pool counts as needed for your environment.
