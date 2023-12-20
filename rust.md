```
(lldb) bt
* thread #1, name = 'cxx_test', stop reason = breakpoint 1.1
  * frame #0: 0x000055555555d39e cxx_test`cxx_test::ffi::BlobstoreClient::put::h8a50f4967eceeb2e(self=0x00005555555bebb0, parts=0x00007fffffffde60) at main.rs:30:12
    frame #1: 0x000055555555dcf2 cxx_test`cxx_test::main::hfbb19916d9bdfe0c at main.rs:40:18
    frame #2: 0x000055555555d79b cxx_test`core::ops::function::FnOnce::call_once::h71a3523acafffe20((null)=(cxx_test`cxx_test::main::hfbb19916d9bdfe0c at main.rs:34), (null)=<unavailable>) at function.rs:250:5
    frame #3: 0x000055555555e26e cxx_test`std::sys_common::backtrace::__rust_begin_short_backtrace::h4a911bd82b3f2ac8(f=(cxx_test`cxx_test::main::hfbb19916d9bdfe0c at main.rs:34)) at backtrace.rs:135:18
    frame #4: 0x000055555555def1 cxx_test`std::rt::lang_start::_$u7b$$u7b$closure$u7d$$u7d$::hcc0a63cf98bc99b4 at rt.rs:166:18
    frame #5: 0x0000555555573ac5 cxx_test`std::rt::lang_start_internal::hf502095b101390bb [inlined] core::ops::function::impls::_$LT$impl$u20$core..ops..function..FnOnce$LT$A$GT$$u20$for$u20$$RF$F$GT$::call_once::h802b0fdd426a12ca at function.rs:284:13
    frame #6: 0x0000555555573ab7 cxx_test`std::rt::lang_start_internal::hf502095b101390bb [inlined] std::panicking::try::do_call::h2a2f25050efa0cf8 at panicking.rs:500:40
    frame #7: 0x0000555555573ab7 cxx_test`std::rt::lang_start_internal::hf502095b101390bb [inlined] std::panicking::try::h9ca7f841c0f0e3dd at panicking.rs:464:19
    frame #8: 0x0000555555573ab7 cxx_test`std::rt::lang_start_internal::hf502095b101390bb [inlined] std::panic::catch_unwind::h92d42a62587f8121 at panic.rs:142:14
    frame #9: 0x0000555555573ab7 cxx_test`std::rt::lang_start_internal::hf502095b101390bb [inlined] std::rt::lang_start_internal::_$u7b$$u7b$closure$u7d$$u7d$::hf1926c7a173d562c at rt.rs:148:48
    frame #10: 0x0000555555573ab7 cxx_test`std::rt::lang_start_internal::hf502095b101390bb [inlined] std::panicking::try::do_call::haac70d88f0cce898 at panicking.rs:500:40
    frame #11: 0x0000555555573ab7 cxx_test`std::rt::lang_start_internal::hf502095b101390bb [inlined] std::panicking::try::h5c20719e1031e74b at panicking.rs:464:19
    frame #12: 0x0000555555573ab7 cxx_test`std::rt::lang_start_internal::hf502095b101390bb [inlined] std::panic::catch_unwind::h9b15b36860d5fe4a at panic.rs:142:14
    frame #13: 0x0000555555573ab7 cxx_test`std::rt::lang_start_internal::hf502095b101390bb at rt.rs:148:20
    frame #14: 0x000055555555deca cxx_test`std::rt::lang_start::h83963faa585edf35(main=(cxx_test`cxx_test::main::hfbb19916d9bdfe0c at main.rs:34), argc=1, argv=0x00007fffffffe218, sigpipe='\0') at rt.rs:165:17
    frame #15: 0x000055555555ddfe cxx_test`main + 30
    frame #16: 0x00007ffff7823a90 libc.so.6`___lldb_unnamed_symbol3152 + 128
    frame #17: 0x00007ffff7823b49 libc.so.6`__libc_start_main + 137
    frame #18: 0x000055555555c9c5 cxx_test`_start + 37
(lldb) frame variable 
```

