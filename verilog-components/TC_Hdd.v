module TC_Hdd (clk, rst, seek, load, save, in, out);
    parameter MEM_WORDS = 256;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [63:0] seek;
    input load;
    input save;
    input [63:0] in;
    output [63:0] out;
    
    reg [63:0] mem [0:MEM_WORDS-1];
    reg [63:0] mp;
    
    initial begin
        hexfile <= HEX_FILE;
        if ($value$plusargs(ARG_SIG, hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
        end else begin
            $display("no file specified");
            for (i=0; i<MEM_WORDS; i=i+1) mem[i] <= {BIT_WIDTH{1'b0}};
        end
        out = {64{1'b0}};
    end

    always @ (posedge clk) begin
        if (rst) begin
            mp = {64{1'b0}};
            out = {64{1'b0}};
        end else begin
            mp <= mp + seek;
            if (load) begin
                out <= mem[mp];
            end
        end
    end
    
    always @ (negedge clk) begin
        if (save && !rst) begin
            mem[mp] <= in;
        end
    end
endmodule
